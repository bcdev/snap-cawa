package org.esa.snap.dataio.nc4;

import org.esa.snap.core.dataio.ProductIO;
import org.esa.snap.core.datamodel.Product;

import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SnapCawaNc4WriterTest {

    public static void main(String[] args) throws Exception {
        final String tcwvFilename = "subset_TCWV.nc";
        final String tcwvFilePath = SnapCawaNc4WriterTest.class.getResource(tcwvFilename).getPath();
        final Product tcwvProduct = loadTcwvProduct(tcwvFilePath);
        final String tcwvCawaNc4Filename = "subset_TCWV_cawa_nc4.nc";
        final String tcwvCawaNc4FilePath = new File(tcwvFilePath).getParent() + File.separator + tcwvCawaNc4Filename;
        Logger.getGlobal().log(Level.INFO, "Writing TCWV CAWA NetCDF4 file '" + tcwvCawaNc4FilePath + "'...");
        ProductIO.writeProduct(tcwvProduct, tcwvCawaNc4FilePath, "NetCDF4-CAWA");
    }

    private static Product loadTcwvProduct(String tcwvFilePath) {
        Product tcwvProduct = null;
        try {
            Logger.getGlobal().log(Level.INFO, "Reading TCWV file '" + tcwvFilePath + "'...");
            tcwvProduct = ProductIO.readProduct(new File(tcwvFilePath));
        } catch (IOException e) {
            Logger.getGlobal().log(Level.WARNING, "Warning: cannot open or read AOT climatology file.");
        }
        return tcwvProduct;
    }
}
